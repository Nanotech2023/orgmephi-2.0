import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { Observable, of } from 'rxjs'
import { SelfUnfilledResponse } from '@api/users/models'
import { catchError, switchMap } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { UsersService } from '@api/users/users.service'
import { Contest, SimpleContest } from '@api/tasks/model'
import { TasksService } from '@api/tasks/tasks.service'


export interface ContestDetailsState
{
    contest?: Contest
    unfilledProfile?: Array<object>
    callState: CallState
}


const initialState: ContestDetailsState = {
    contest: undefined,
    unfilledProfile: undefined,
    callState: LoadingState.INIT
}


@Injectable()
export class ContestDetailsStore extends ComponentStore<ContestDetailsState>
{
    constructor( private usersService: UsersService, private tasksService: TasksService )
    {
        super( initialState )
    }

    readonly isFilledProfile$: Observable<boolean> = this.select( state => state.unfilledProfile === undefined || !state.unfilledProfile.length )
    readonly contest$: Observable<SimpleContest | undefined> = this.select( state => state.contest as SimpleContest )

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    // UPDATERS
    readonly updateError = this.updater( ( state: ContestDetailsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestDetailsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestDetailsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setUnfilledProfile = this.updater( ( state: ContestDetailsState, unfilledProfile: object[] | undefined ) =>
        ( {
            ...state,
            unfilledProfile: unfilledProfile
        } ) )

    readonly setContest = this.updater( ( state: ContestDetailsState, contest: Contest ) =>
        ( {
            ...state,
            contest: contest
        } ) )

    // EFFECTS
    readonly fetchUnfilledProfile = this.effect( () =>
    {
        this.setLoading()
        return this.usersService.userProfileUnfilledGet().pipe(
            tapResponse(
                ( response: SelfUnfilledResponse ) => this.setUnfilledProfile( response.unfilled ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
        )
    } )

    readonly fetchSingle = this.effect( ( contestId$: Observable<number> ) =>
        contestId$.pipe(
            switchMap( ( contestId: number ) =>
                this.tasksService.tasksParticipantOlympiadIdOlympiadGet( contestId ).pipe(
                    tapResponse(
                        ( response: Contest ) => this.setContest( response ),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) ) )
        ) )
}

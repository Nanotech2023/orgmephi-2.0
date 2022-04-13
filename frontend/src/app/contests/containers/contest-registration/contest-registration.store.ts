import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { EMPTY, Observable, of } from 'rxjs'
import { catchError, switchMap, tap } from 'rxjs/operators'
import { Contest, EnrollRequestTaskParticipant, SimpleContest } from '@api/tasks/model'
import { displayErrorMessage } from '@/shared/logging'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { Router } from '@angular/router'


export interface ContestRegistrationState
{
    contest?: Contest
    callState: CallState
}


const initialState: ContestRegistrationState = {
    contest: undefined,
    callState: LoadingState.INIT
}


@Injectable()
export class ContestRegistrationStore extends ComponentStore<ContestRegistrationState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService, private router: Router )
    {
        super( initialState )
    }

    readonly contest$: Observable<SimpleContest | undefined> = this.select( state => state.contest as SimpleContest )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    // UPDATERS
    readonly updateError = this.updater( ( state: ContestRegistrationState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestRegistrationState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestRegistrationState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setContest = this.updater( ( state: ContestRegistrationState, contest: Contest ) =>
        ( {
            ...state,
            contest: contest
        } ) )

    // EFFECTS
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


    readonly enroll = this.effect( ( enroll$: Observable<{ contestId: number, locationId: number }> ) =>
        enroll$.pipe(
            switchMap( ( enroll: { contestId: number, locationId: number } ) =>
            {
                const { contestId, locationId } = enroll
                const enrollRequestTaskParticipant: EnrollRequestTaskParticipant = { location_id: locationId }
                return this.tasksService.tasksParticipantContestIdContestEnrollPost( contestId, enrollRequestTaskParticipant ).pipe(
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
                    switchMap( () =>
                        this.responsesService.responsesParticipantContestContestIdUserSelfCreatePost( contestId ).pipe(
                            catchError( ( error: any ) => of( EMPTY ) ),
                            tap( () => this.router.navigate( [ `/contests/${ contestId }/assignment` ] ) )
                        ) ) )
            } )
        ) )
}

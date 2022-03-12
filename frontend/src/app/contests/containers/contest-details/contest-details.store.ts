import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { EMPTY, Observable, of } from 'rxjs'
import { SelfUnfilledResponse } from '@api/users/models'
import { catchError, switchMap } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { UsersService } from '@api/users/users.service'
import { Contest, SimpleContest, UserProctoringDataResponseTaskParticipant } from '@api/tasks/model'
import { TasksService } from '@api/tasks/tasks.service'
import {
    AllUserResultsResponse,
    UserResultsForContestResponse
} from '@api/responses/model'
import { ResponsesService } from '@api/responses/responses.service'


export interface ContestDetailsState
{
    contest?: Contest
    unfilledProfile?: Array<object>
    result?: UserResultsForContestResponse[]
    proctoringData?: UserProctoringDataResponseTaskParticipant
    callState: CallState
}


const initialState: ContestDetailsState = {
    contest: undefined,
    unfilledProfile: undefined,
    result: undefined,
    proctoringData: undefined,
    callState: LoadingState.INIT
}


@Injectable()
export class ContestDetailsStore extends ComponentStore<ContestDetailsState>
{
    constructor( private usersService: UsersService, private tasksService: TasksService, private responsesService: ResponsesService )
    {
        super( initialState )
    }

    readonly isFilledProfile$: Observable<boolean> = this.select( state => state.unfilledProfile === undefined || !state.unfilledProfile.length )
    readonly contest$: Observable<SimpleContest | undefined> = this.select( state => state.contest as SimpleContest )
    readonly contestResult$: Observable<UserResultsForContestResponse | undefined> = this.select( state => state.result?.find( item => item.contest_info.contest_id == state.contest?.contest_id ) )
    readonly contestProctoringData$: Observable<UserProctoringDataResponseTaskParticipant | undefined> = this.select( state => state.proctoringData )

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

    readonly setResults = this.updater( ( state: ContestDetailsState, results: UserResultsForContestResponse[] ) =>
        ( {
            ...state,
            results: results
        } ) )

    readonly setProctoringData = this.updater( ( state: ContestDetailsState, proctoringData: UserProctoringDataResponseTaskParticipant ) =>
        ( {
            ...state,
            proctoringData: proctoringData
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

    readonly fetchProctoringData = this.effect( ( contestId$: Observable<number> ) =>
        contestId$.pipe(
            switchMap( ( contestId: number ) =>
                this.tasksService.tasksParticipantContestIdContestProctorDataGet( contestId ).pipe(
                    tapResponse(
                        ( response: UserProctoringDataResponseTaskParticipant ) => this.setProctoringData( response ),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( ( error: any ) => EMPTY ) ) ) ) )


    readonly fetchAllResults = this.effect( () =>
    {
        this.setLoading()
        return this.responsesService.responsesParticipantContestUserSelfResultsGet().pipe(
            tapResponse(
                ( response: AllUserResultsResponse ) => this.setResults( response.results ?? [] ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( ( error: any ) => EMPTY ) )
    } )
}
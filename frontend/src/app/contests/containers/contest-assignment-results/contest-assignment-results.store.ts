import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { Contest } from '@api/tasks/model'
import { UserResultForContestResponse } from '@api/responses/model'
import { Observable, of } from 'rxjs'
import { catchError, switchMap } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'


export interface ContestAssignmentResultsState
{
    callState: CallState,
    contest?: Contest
    results?: UserResultForContestResponse
}


const initialState: ContestAssignmentResultsState = {
    callState: LoadingState.INIT,
    contest: undefined,
    results: undefined
}


@Injectable()
export class ContestAssignmentResultsStore extends ComponentStore<ContestAssignmentResultsState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService )
    {
        super( initialState )
    }

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )
    private readonly contest$: Observable<Contest | undefined> = this.select( state => state.contest )
    private readonly results$: Observable<UserResultForContestResponse | undefined> = this.select( state => state.results )

    readonly viewModel$: Observable<{ loading: boolean; error: string | null, contest: Contest | undefined, results: UserResultForContestResponse | undefined }> = this.select(
        this.loading$,
        this.error$,
        this.contest$,
        this.results$,
        ( loading, error, contest, results ) =>
            ( {
                loading: loading,
                error: error,
                contest: contest,
                results: results
            } )
    )

    // UPDATERS
    readonly updateError = this.updater( ( state: ContestAssignmentResultsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestAssignmentResultsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestAssignmentResultsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setContest = this.updater( ( state: ContestAssignmentResultsState, contest: Contest ) =>
        ( {
            ...state,
            contest: contest
        } ) )

    readonly setResults = this.updater( ( state: ContestAssignmentResultsState, response: UserResultForContestResponse ) =>
        ( {
            ...state,
            results: response
        } ) )


    // EFFECTS
    readonly fetchContest = this.effect( ( contestId$: Observable<number> ) =>
        contestId$.pipe(
            switchMap( ( id: number ) =>
                this.tasksService.tasksParticipantOlympiadIdOlympiadGet( id ).pipe(
                    tapResponse(
                        ( response ) => this.setContest( response ),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                ) )
        ) )


    readonly fetchResults = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contestId: number ) =>
                this.responsesService.responsesParticipantContestContestIdUserSelfResultsGet( contestId ).pipe(
                    tapResponse(
                        ( response: UserResultForContestResponse ) => this.setResults( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
    } )
}

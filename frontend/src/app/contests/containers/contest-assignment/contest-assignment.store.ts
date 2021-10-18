import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { AllTaskResponseTaskParticipant, Contest, TaskForUserResponseTaskParticipant, Variant } from '@api/tasks/model'
import { catchError, switchMap } from 'rxjs/operators'
import { EMPTY, Observable } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { UserTimeResponseRequest } from '@api/responses/model'


export interface ContestAssignmentState
{
    callState: CallState,
    contest?: Contest
    variant?: Variant
    tasks: Array<TaskForUserResponseTaskParticipant>
    time?: number
}


const initialState: ContestAssignmentState =
    {
        callState: LoadingState.INIT,
        contest: undefined,
        variant: undefined,
        tasks: [],
        time: undefined
    }


@Injectable()
export class ContestAssignmentStore extends ComponentStore<ContestAssignmentState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService )
    {
        super( initialState )
    }

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )
    private readonly contest$: Observable<Contest | undefined> = this.select( state => state.contest )
    private readonly variant$: Observable<Variant | undefined> = this.select( state => state.variant )
    private readonly tasks$: Observable<Array<TaskForUserResponseTaskParticipant>> = this.select( state => state.tasks )
    private readonly time$: Observable<number | undefined> = this.select( state => state.time )

    readonly viewModel$: Observable<{ loading: boolean; error: string | null, contest: Contest | undefined, variant: Variant | undefined, tasks: Array<TaskForUserResponseTaskParticipant>, time: number | undefined }> = this.select(
        this.loading$,
        this.error$,
        this.contest$,
        this.variant$,
        this.tasks$,
        this.time$,
        ( loading, error, contest, variant, tasks, time ) =>
            ( {
                loading: loading,
                error: error,
                contest: contest,
                variant: variant,
                tasks: tasks,
                time: time
            } )
    )

    // UPDATERS
    readonly updateError = this.updater( ( state: ContestAssignmentState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestAssignmentState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestAssignmentState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setContest = this.updater( ( state: ContestAssignmentState, contest: Contest ) =>
        ( {
            ...state,
            contest: contest
        } ) )

    readonly setVariant = this.updater( ( state: ContestAssignmentState, variant: Variant ) =>
        ( {
            ...state,
            variant: variant
        } ) )

    readonly setTasks = this.updater( ( state: ContestAssignmentState, response: AllTaskResponseTaskParticipant ) =>
        ( {
            ...state,
            tasks: response.tasks_list
        } ) )

    readonly setTime = this.updater( ( state: ContestAssignmentState, response: UserTimeResponseRequest ) =>
        ( {
            ...state,
            time: response.time
        } ) )

    // EFFECTS
    readonly fetchTasks = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contest: number ) =>
                this.tasksService.tasksParticipantContestIdContestTasksSelfGet( contest ).pipe(
                    tapResponse(
                        ( response: AllTaskResponseTaskParticipant ) => this.setTasks( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( () => EMPTY ) )
    } )

    readonly fetchContest = this.effect( ( contestId$: Observable<number> ) =>
        contestId$.pipe(
            switchMap( ( id: number ) =>
                this.tasksService.tasksParticipantOlympiadIdOlympiadGet( id ).pipe(
                    tapResponse(
                        ( response ) => this.setContest( response ),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( () => EMPTY )
                ) )
        ) )

    readonly fetchVariant = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contest: number ) =>
                this.tasksService.tasksParticipantContestIdContestVariantSelfGet( contest ).pipe(
                    tapResponse(
                        ( response: Variant ) => this.setVariant( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( () => EMPTY ) )
    } )

    readonly fetchTime = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contest: number ) =>
                this.responsesService.responsesParticipantContestContestIdUserSelfTimeGet( contest ).pipe(
                    tapResponse(
                        ( response: UserTimeResponseRequest ) => this.setTime( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( () => EMPTY ) )
    } )


}

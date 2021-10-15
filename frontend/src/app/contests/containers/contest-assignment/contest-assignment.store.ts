import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { AllTaskResponseTaskParticipant, Contest, TaskForUserResponseTaskParticipant, Variant } from '@api/tasks/model'
import { catchError, switchMap } from 'rxjs/operators'
import { EMPTY, Observable } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { TasksService } from '@api/tasks/tasks.service'


export interface ContestAssignmentState
{
    callState: CallState,
    variant?: Variant
    contest?: Contest
    tasks: Array<TaskForUserResponseTaskParticipant>
}


const initialState: ContestAssignmentState =
    {
        callState: LoadingState.INIT,
        variant: undefined,
        contest: undefined,
        tasks: []
    }


@Injectable()
export class ContestAssignmentStore extends ComponentStore<ContestAssignmentState>
{
    constructor( private tasksService: TasksService )
    {
        super( initialState )
    }

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )
    readonly contest$: Observable<Contest | undefined> = this.select( state => state.contest )
    readonly variant$: Observable<Variant | undefined> = this.select( state => state.variant )
    readonly tasks$: Observable<Array<TaskForUserResponseTaskParticipant>> = this.select( state => state.tasks )

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

    // EFFECTS
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


}

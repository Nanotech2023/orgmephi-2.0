import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import {
    AllTaskResponseTaskParticipant,
    Contest,
    TaskForUserResponseTaskParticipant,
    VariantWithCompletedTasksCountTaskParticipant
} from '@api/tasks/model'
import { catchError, switchMap, tap } from 'rxjs/operators'
import { Observable, of } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { UserResponseStatusResponse, UserResultForContestResponse, UserTimeResponseRequest } from '@api/responses/model'
import { Router } from '@angular/router'
import { displayErrorMessage } from '@/shared/logging'


export interface ContestAssignmentState
{
    callState: CallState,
    contest?: Contest
    variant?: VariantWithCompletedTasksCountTaskParticipant
    tasks: Array<TaskForUserResponseTaskParticipant>
    time?: number,
    status?: UserResponseStatusResponse.StatusEnum,
    results?: UserResultForContestResponse
}


const initialState: ContestAssignmentState =
    {
        callState: LoadingState.INIT,
        contest: undefined,
        variant: undefined,
        tasks: [],
        time: undefined,
        status: undefined,
        results: undefined
    }


@Injectable()
export class ContestAssignmentStore extends ComponentStore<ContestAssignmentState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService, private router: Router )
    {
        super( initialState )
    }

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )
    private readonly contest$: Observable<Contest | undefined> = this.select( state => state.contest )
    private readonly variant$: Observable<VariantWithCompletedTasksCountTaskParticipant | undefined> = this.select( state => state.variant )
    private readonly tasks$: Observable<Array<TaskForUserResponseTaskParticipant>> = this.select( state => state.tasks )
    private readonly time$: Observable<number | undefined> = this.select( state => state.time )
    private readonly status$: Observable<UserResponseStatusResponse.StatusEnum | undefined> = this.select( state => state.status )

    readonly viewModel$: Observable<{ loading: boolean; error: string | null, contest: Contest | undefined, variant: VariantWithCompletedTasksCountTaskParticipant | undefined, tasks: Array<TaskForUserResponseTaskParticipant>, time: number | undefined, status: UserResponseStatusResponse.StatusEnum | undefined }> = this.select(
        this.loading$,
        this.error$,
        this.contest$,
        this.variant$,
        this.tasks$,
        this.time$,
        this.status$,
        ( loading, error, contest, variant, tasks, time, status ) =>
            ( {
                loading: loading,
                error: error,
                contest: contest,
                variant: variant,
                tasks: tasks,
                time: time,
                status: status
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

    readonly setVariant = this.updater( ( state: ContestAssignmentState, variant: VariantWithCompletedTasksCountTaskParticipant ) =>
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

    readonly setStatus = this.updater( ( state: ContestAssignmentState, response: UserResponseStatusResponse ) =>
        ( {
            ...state,
            status: response.status
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
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
    } )

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

    readonly fetchVariant = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contest: number ) =>
                this.tasksService.tasksParticipantContestIdContestVariantSelfGet( contest ).pipe(
                    tapResponse(
                        ( response: VariantWithCompletedTasksCountTaskParticipant ) => this.setVariant( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
    } )

    readonly fetchTime = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contestId: number ) =>
                this.responsesService.responsesParticipantContestContestIdUserSelfTimeGet( contestId ).pipe(
                    tapResponse(
                        ( response: UserTimeResponseRequest ) => this.setTime( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
    } )

    readonly fetchStatus = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contestId: number ) =>
                this.responsesService.responsesParticipantContestContestIdUserSelfStatusGet( contestId ).pipe(
                    tapResponse(
                        ( response: UserResponseStatusResponse ) => this.setStatus( response ),
                        ( error: string ) => this.updateError( error )
                    )
                )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
    } )

    readonly finish = this.effect( ( contestId$: Observable<number> ) =>
    {
        this.setLoading()
        return contestId$.pipe( switchMap( ( contestId: number ) =>
                this.responsesService.responsesParticipantContestContestIdUserSelfFinishPost( contestId ).pipe(
                    tapResponse(
                        ( response: UserTimeResponseRequest ) => this.setTime( response ),
                        ( error: string ) => this.updateError( error )
                    ),
                    tap( () => this.router.navigate( [ `/contests/${ contestId }/registration` ] ) )
                )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
    } )
}

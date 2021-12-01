import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { TasksService } from '@api/tasks/tasks.service'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable, of } from 'rxjs'
import {
    CompositeContest,
    Contest,
    EnrollRequestTaskParticipant,
    FilterSimpleContestResponseTaskParticipant,
    OlympiadLocation,
    SimpleContest,
    SimpleContestWithFlagResponseTaskParticipant
} from '@api/tasks/model'
import { catchError, switchMap } from 'rxjs/operators'
import { ResponsesService } from '@api/responses/responses.service'
import CompositeTypeEnum = SimpleContest.CompositeTypeEnum
import { displayErrorMessage } from '@/shared/logging'


export interface ContestsState
{
    contests: Array<SimpleContestWithFlagResponseTaskParticipant>
    locations: Array<OlympiadLocation>
    contest?: Contest
    callState: CallState
}


const initialState: ContestsState =
    {
        contests: [],
        locations: [],
        contest: undefined,
        callState: LoadingState.INIT
    }


@Injectable()
export class ContestsStore extends ComponentStore<ContestsState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService )
    {
        super( initialState )
    }

    readonly contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]> = this.select( state => state.contests.filter( item => item.contest?.composite_type === CompositeTypeEnum.SimpleContest ) )
    readonly contest$: Observable<SimpleContest | undefined> = this.select( state => state.contest as SimpleContest )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )


    // UPDATERS
    readonly updateError = this.updater( ( state: ContestsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setContests = this.updater( ( state: ContestsState, contests: Array<SimpleContestWithFlagResponseTaskParticipant> ) =>
        ( {
            ...state,
            error: "",
            contests: [ ...state.contests, ...contests ]
        } ) )

    readonly selectContest = this.updater( ( state: ContestsState, contest: Contest ) =>
        ( {
            ...state,
            contest: contest
        } ) )

    // EFFECTS
    readonly fetchAll = this.effect( () =>
    {
        this.setLoading()
        return this.tasksService.tasksParticipantOlympiadAllGet().pipe(
            tapResponse(
                ( response: FilterSimpleContestResponseTaskParticipant ) => this.setContests( response.contest_list ?? [] ),
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
                        ( response: Contest ) => this.selectContest( response ),
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
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                )
            } )
        ) )

    readonly start = this.effect( ( contestId$: Observable<number> ) =>
        contestId$.pipe(
            switchMap( ( contestId: number ) =>
                this.responsesService.responsesParticipantContestContestIdUserSelfCreatePost( contestId ).pipe(
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                ) )
        ) )
}
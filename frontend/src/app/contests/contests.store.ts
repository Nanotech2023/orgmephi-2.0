import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { TasksService } from '@api/tasks/tasks.service'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable } from 'rxjs'
import {
    AllLocationResponseTaskUnauthorized,
    AllOlympiadsResponseTaskUnauthorized,
    Contest,
    EnrollRequestTaskParticipant,
    OlympiadLocation,
    Variant
} from '@api/tasks/model'
import { catchError, switchMap } from 'rxjs/operators'


export interface ContestsState
{
    contests: Array<Contest>
    locations: Array<OlympiadLocation>
    selectedContest?: Contest
    selectedVariant?: Variant
    callState: CallState
}


const initialState: ContestsState = {
    contests: [],
    locations: [],
    selectedVariant: undefined,
    selectedContest: undefined,
    callState: LoadingState.INIT
}


@Injectable()
export class ContestsStore extends ComponentStore<ContestsState>
{
    constructor( private tasksService: TasksService )
    {
        super( initialState )
    }

    readonly contests: Observable<Contest[]> = this.select( state => state.contests )
    readonly selectedContest: Observable<Contest | undefined> = this.select( state => state.selectedContest )
    readonly locations: Observable<Contest | undefined> = this.select( state => state.selectedContest )
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

    readonly setContests = this.updater( ( state: ContestsState, contests: Array<Contest> ) =>
        ( {
            ...state,
            error: "",
            contests: [ ...state.contests, ...contests ]
        } ) )

    readonly selectContest = this.updater( ( state: ContestsState, contest: Contest ) =>
        ( {
            ...state,
            selectedContest: contest
        } ) )

    readonly setVariant = this.updater( ( state: ContestsState, variant: Variant ) =>
        ( {
            ...state,
            variant: variant
        } ) )


    readonly setLocations = this.updater( ( state: ContestsState, locations: Array<OlympiadLocation> ) =>
        ( {
            ...state,
            locations: locations
        } ) )
    // EFFECTS

    readonly fetchAll = this.effect( () =>
    {
        this.setLoading()
        this.tasksService.tasksUnauthorizedLocationAllGet().pipe(
            tapResponse(
                ( response: AllLocationResponseTaskUnauthorized ) => this.setLocations( response.locations ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
        return this.tasksService.tasksParticipantOlympiadAllGet().pipe(
            tapResponse(
                ( response: AllOlympiadsResponseTaskUnauthorized ) => this.setContests( response.contest_list ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )

    readonly getVariant = this.effect( ( contestId$: Observable<number> ) =>
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

    // readonly fetchSingle = this.effect( ( contestId$: Observable<number> ) =>
    //     contestId$.pipe(
    //         switchMap( ( id: number ) =>
    //             this.tasksService.tasksParticipantOlympiadIdOlympiadGet( id ).pipe(
    //                 tapResponse(
    //                     ( response ) => this.selectContest( response ),
    //                     ( error: string ) => this.updateError( error )
    //                 ),
    //                 catchError( () => EMPTY )
    //             ) )
    //     ) )

    readonly enroll = this.effect( ( contest$: Observable<{ contestId: number, enrollRequestTaskParticipant: EnrollRequestTaskParticipant }> ) =>
        contest$.pipe(
            switchMap( ( contest: { contestId: number; enrollRequestTaskParticipant: EnrollRequestTaskParticipant } ) =>
                this.tasksService.tasksParticipantContestIdContestEnrollPost( contest.contestId, contest.enrollRequestTaskParticipant ).pipe(
                    catchError( () => EMPTY )
                ) )
        ) )
}
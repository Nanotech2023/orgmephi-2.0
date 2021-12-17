import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { TasksService } from '@api/tasks/tasks.service'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable, of } from 'rxjs'
import {
    Contest,
    EnrollRequestTaskParticipant,
    FilterSimpleContestResponseTaskParticipant,
    OlympiadLocation,
    SimpleContest,
    SimpleContestWithFlagResponseTaskParticipant
} from '@api/tasks/model'
import { catchError, switchMap, tap } from 'rxjs/operators'
import { ResponsesService } from '@api/responses/responses.service'
import { displayErrorMessage } from '@/shared/logging'
import { UsersService } from '@api/users/users.service'
import { SelfUnfilledResponse } from '@api/users/models'
import { Router } from '@angular/router'
import CompositeTypeEnum = SimpleContest.CompositeTypeEnum


export interface ContestsState
{
    contests: Array<SimpleContestWithFlagResponseTaskParticipant>
    locations: Array<OlympiadLocation>
    contest?: Contest
    callState: CallState
    unfilledProfile?: Array<object>
}


const initialState: ContestsState =
    {
        contests: [],
        locations: [],
        contest: undefined,
        callState: LoadingState.INIT,
        unfilledProfile: undefined
    }


@Injectable()
export class ContestsStore extends ComponentStore<ContestsState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService, private usersService: UsersService, private router: Router )
    {
        super( initialState )
    }

    readonly contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]> = this.select( state => state.contests.filter( item =>
    {
        return item.contest !== undefined
    } ) )
    readonly contest$: Observable<SimpleContest | undefined> = this.select( state => state.contest as SimpleContest )
    readonly isFilledProfile$: Observable<boolean> = this.select( state => state.unfilledProfile === undefined || !state.unfilledProfile.length )
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

    readonly setUnfilledProfile = this.updater( ( state: ContestsState, unfilledProfile: object[] | undefined ) =>
        ( {
            ...state,
            unfilledProfile: unfilledProfile
        } ) )

    // EFFECTS
    readonly fetchAll = this.effect( ( userGrade$: Observable<number> ) =>
        userGrade$.pipe(
            switchMap( ( userGrade: number ) =>
            {
                return this.tasksService.tasksParticipantOlympiadAllGet( true, undefined, undefined, undefined, undefined, 2021, undefined, undefined, undefined, CompositeTypeEnum.SimpleContest ).pipe(
                    tapResponse(
                        ( response: FilterSimpleContestResponseTaskParticipant ) => this.setContests( response.contest_list?.filter( item => this.filterContest( item, userGrade ) ) ?? [] ),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                )
            } ) ) )

    filterContest( item: SimpleContestWithFlagResponseTaskParticipant, userGrade: number )
    {
        if ( item.contest === undefined )
            return false
        if ( item.contest.base_contest.target_classes === undefined )
            return false
        return item.contest.base_contest.target_classes.some( targetClass => targetClass.target_class == userGrade.toString() )
    }

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
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
                    switchMap( () =>
                        this.responsesService.responsesParticipantContestContestIdUserSelfCreatePost( contestId ).pipe(
                            catchError( ( error: any ) => of( EMPTY ) ),
                            tap( () => this.router.navigate( [ `/contests/${ contestId }/assignment` ] ) )
                        ) ) )
            } )
        ) )

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
}
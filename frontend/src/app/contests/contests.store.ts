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
import { catchError, filter, map, switchMap, tap, withLatestFrom } from 'rxjs/operators'
import { ResponsesService } from '@api/responses/responses.service'
import CompositeTypeEnum = SimpleContest.CompositeTypeEnum
import { displayErrorMessage } from '@/shared/logging'
import { Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { UsersService } from '@api/users/users.service'
import { SchoolInfo, SelfUnfilledResponse } from '@api/users/models'
import { Router } from '@angular/router'


export interface ContestsState
{
    contests: Array<SimpleContestWithFlagResponseTaskParticipant>
    locations: Array<OlympiadLocation>
    contest?: Contest
    callState: CallState
    schoolInfo?: SchoolInfo
    unfilledProfile?: Array<object>
}


const initialState: ContestsState =
    {
        contests: [],
        locations: [],
        contest: undefined,
        callState: LoadingState.INIT,
        schoolInfo: undefined,
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
        if ( item.contest === undefined )
            return false
        if ( item.contest.composite_type !== CompositeTypeEnum.SimpleContest )
            return false
        if ( state.schoolInfo?.grade === undefined )
            return true
        if ( item.contest.base_contest.target_classes === undefined )
            return true
        return item.contest.base_contest.target_classes.some( targetClass => targetClass.target_class == state.schoolInfo!.grade!.toString() )
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

    readonly setSchoolInfo = this.updater( ( state: ContestsState, schoolInfo: SchoolInfo ) =>
        ( {
            ...state,
            schoolInfo: schoolInfo
        } ) )

    readonly setUnfilledProfile = this.updater( ( state: ContestsState, unfilledProfile: object[] | undefined ) =>
        ( {
            ...state,
            unfilledProfile: unfilledProfile
        } ) )

    // EFFECTS
    readonly fetchAll = this.effect( () =>
    {
        this.setLoading()
        return this.tasksService.tasksParticipantOlympiadAllGet( undefined, undefined, undefined, undefined, 2021 ).pipe(
            tapResponse(
                ( response: FilterSimpleContestResponseTaskParticipant ) => this.setContests( response.contest_list ?? [] ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
        )
    } )

    readonly fetchSchoolInfo = this.effect( () =>
    {
        this.setLoading()
        return this.usersService.userProfileSchoolGet().pipe(
            tapResponse(
                ( response: SchoolInfo ) => this.setSchoolInfo( response ),
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
                ).pipe(
                    switchMap( () =>
                        this.responsesService.responsesParticipantContestContestIdUserSelfCreatePost( contestId ).pipe(
                            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
                            tap( () => this.router.navigate( [ `/contests/${ contestId }/assignment` ] ) )
                        ) )
                )
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
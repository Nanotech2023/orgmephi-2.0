import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { EMPTY, Observable, zip } from 'rxjs'
import {
    AllTaskResponseTaskParticipant,
    FilterSimpleContestResponseTaskParticipant,
    SimpleContestWithFlagResponseTaskParticipant
} from '@api/tasks/model'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { ManageContestsState } from '@/manage-contests/manage-contests.store'
import { catchError, finalize, switchMap } from 'rxjs/operators'
import { ActivatedRoute } from '@angular/router'
import {
    AllUserAnswersResponse,
    AllUserMarksResponse,
    UserResponseStatusResponse,
    UserTimeResponseRequest
} from '@api/responses/model'
import { ResponsesService } from '@api/responses/responses.service'


export interface ManageContestUserAssignmentState
{
    simpleContestId?: number
    userId?: number
    userResponse?: AllUserAnswersResponse
    userStatus?: UserResponseStatusResponse
    userMark?: AllUserMarksResponse
    userTime?: UserTimeResponseRequest
    userExtraTime?: UserTimeResponseRequest
    callState: CallState
}


const initialState: ManageContestUserAssignmentState =
    {
        simpleContestId: undefined,
        userId: undefined,
        userResponse: undefined,
        userStatus: undefined,
        userMark: undefined,
        userTime: undefined,
        userExtraTime: undefined,
        callState: LoadingState.INIT
    }


@Injectable()
export class ManageContestUserAssignmentStore extends ComponentStore<ManageContestUserAssignmentState>
{
    constructor( private responsesService: ResponsesService )
    {
        super( initialState )
    }

    readonly userResponse$: Observable<AllUserAnswersResponse | undefined> = this.select( state => state.userResponse )
    readonly userStatus$: Observable<UserResponseStatusResponse | undefined> = this.select( state => state.userStatus )
    readonly userMark$: Observable<AllUserMarksResponse | undefined> = this.select( state => state.userMark )
    readonly userTime$: Observable<UserTimeResponseRequest | undefined> = this.select( state => state.userTime )
    readonly userExtraTime$: Observable<UserTimeResponseRequest | undefined> = this.select( state => state.userExtraTime )

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    readonly viewModel$ = this.select(
        this.userResponse$,
        this.userStatus$,
        this.userMark$,
        this.userTime$,
        this.userExtraTime$,
        this.loading$,
        this.error$,
        ( userResponse$, userStatus$, userMark$, userTime$, userExtraTime$, loading$, error$ ) => ( {
            userResponse: userResponse$!,
            userStatus: userStatus$!,
            userMark: userMark$!,
            userTime: userTime$!,
            userExtraTime: userExtraTime$!,
            loading: loading$,
            error: error$
        } )
    )


    // UPDATERS
    readonly setInitialData = this.updater( ( state: ManageContestUserAssignmentState, initialData: { simpleContestId: number, userId: number } ) =>
        ( {
            ...state,
            simpleContestId: initialData.simpleContestId,
            userId: initialData.userId
        } ) )

    readonly updateError = this.updater( ( state: ManageContestUserAssignmentState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ManageContestUserAssignmentState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ManageContestUserAssignmentState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )


    // EFFECTS
    readonly fetchUserResponse = this.effect( ( contestUserAssignment$: Observable<{ contestId: number, userId: number }> ) =>
    {
        return contestUserAssignment$.pipe( switchMap( ( contestUserAssignment: { contestId: number, userId: number } ) =>
            this.responsesService.responsesCreatorContestContestIdUserUserIdResponseGet( contestUserAssignment.contestId, contestUserAssignment.userId ).pipe(
                tapResponse(
                    ( response: AllUserAnswersResponse ) =>
                        this.setState( {
                            userResponse: response,
                            callState: LoadingState.LOADED
                        } ),
                    ( error: string ) => this.updateError( error )
                ),
                catchError( () => EMPTY )
            ) ) )
    } )

    readonly fetchUserStatus = this.effect( ( contestUserAssignment$: Observable<{ contestId: number, userId: number }> ) =>
    {
        return contestUserAssignment$.pipe( switchMap( ( contestUserAssignment: { contestId: number, userId: number } ) =>
            this.responsesService.responsesCreatorContestContestIdUserUserIdStatusGet( contestUserAssignment.contestId, contestUserAssignment.userId ).pipe(
                tapResponse(
                    ( response: UserResponseStatusResponse ) =>
                        this.setState( {
                            userStatus: response,
                            callState: LoadingState.LOADED
                        } ),
                    ( error: string ) => this.updateError( error )
                ),
                catchError( () => EMPTY )
            ) ) )
    } )

    readonly fetchUserMark = this.effect( ( contestUserAssignment$: Observable<{ contestId: number, userId: number }> ) =>
    {
        return contestUserAssignment$.pipe( switchMap( ( contestUserAssignment: { contestId: number, userId: number } ) =>
            this.responsesService.responsesCreatorContestContestIdUserUserIdMarkGet( contestUserAssignment.contestId, contestUserAssignment.userId ).pipe(
                tapResponse(
                    ( response: AllUserMarksResponse ) =>
                        this.setState( {
                            userMark: response,
                            callState: LoadingState.LOADED
                        } ),
                    ( error: string ) => this.updateError( error )
                ),
                catchError( () => EMPTY )
            ) ) )
    } )

    readonly fetchUserTime = this.effect( ( contestUserAssignment$: Observable<{ contestId: number, userId: number }> ) =>
    {
        return contestUserAssignment$.pipe( switchMap( ( contestUserAssignment: { contestId: number, userId: number } ) =>
            this.responsesService.responsesCreatorContestContestIdUserUserIdTimeGet( contestUserAssignment.contestId, contestUserAssignment.userId ).pipe(
                tapResponse(
                    ( response: UserTimeResponseRequest ) =>
                        this.setState( {
                            userTime: response,
                            callState: LoadingState.LOADED
                        } ),
                    ( error: string ) => this.updateError( error )
                ),
                catchError( () => EMPTY )
            ) ) )
    } )

    readonly fetchUserExtraTime = this.effect( ( contestUserAssignment$: Observable<{ contestId: number, userId: number }> ) =>
    {
        return contestUserAssignment$.pipe( switchMap( ( contestUserAssignment: { contestId: number, userId: number } ) =>
            this.responsesService.responsesCreatorContestContestIdUserUserIdTimeExtraGet( contestUserAssignment.contestId, contestUserAssignment.userId ).pipe(
                tapResponse(
                    ( response: UserTimeResponseRequest ) =>
                        this.setState( {
                            userExtraTime: response,
                            callState: LoadingState.LOADED
                        } ),
                    ( error: string ) => this.updateError( error )
                ),
                catchError( () => EMPTY )
            ) ) )
    } )
}

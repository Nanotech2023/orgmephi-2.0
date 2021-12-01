import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { EMPTY, Observable, of } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { catchError, switchMap } from 'rxjs/operators'
import {
    AllUserAnswersResponse,
    AllUserMarksResponse,
    AnswerWithoutMark,
    BaseAnswer,
    UserResponseStatusResponse,
    UserTimeResponseRequest
} from '@api/responses/model'
import { ResponsesService } from '@api/responses/responses.service'
import { displayErrorMessage } from '@/shared/logging'


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

    readonly userWorkId$: Observable<number | undefined> = this.select( state => state.userResponse?.work_id )
    readonly userResponse$: Observable<Array<AnswerWithoutMark>> = this.select( state => state.userResponse?.user_answers ?? [] )
    readonly userStatus$: Observable<UserResponseStatusResponse.StatusEnum | undefined> = this.select( state => state.userStatus?.status )
    readonly userMark$: Observable<Array<BaseAnswer>> = this.select( state => state.userMark?.user_answers ?? [] )
    readonly userTime$: Observable<number> = this.select( state => state.userTime?.time ?? 0 )
    readonly userExtraTime$: Observable<number> = this.select( state => state.userExtraTime?.time ?? 0 )

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    readonly viewModel$ = this.select(
        this.userWorkId$,
        this.userResponse$,
        this.userStatus$,
        this.userMark$,
        this.userTime$,
        this.userExtraTime$,
        this.loading$,
        this.error$,
        ( userWorkId$, userResponse$, userStatus$, userMark$, userTime$, userExtraTime$, loading$, error$ ) => ( {
            userWorkId: userWorkId$!,
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
                catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
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
                catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
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
                catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
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
                catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
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
                catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
            ) ) )
    } )
}

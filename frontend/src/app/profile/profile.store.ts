import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import {
    Document,
    Location,
    LocationRussia,
    UserInfo,
    UserLimitations,
    DocumentTypeEnum, LocationTypeEnum, SchoolInfo
} from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { Observable, of, zip } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { catchError, finalize, switchMap, withLatestFrom } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'


export interface ProfileState
{
    userInfo?: UserInfo
    schoolInfo?: SchoolInfo
    profileUnfilled: any
    callState: CallState
}


const initialState: ProfileState = {
    userInfo: undefined,
    schoolInfo: undefined,
    profileUnfilled: null,
    callState: LoadingState.INIT
}


@Injectable()
export class ProfileStore extends ComponentStore<ProfileState>
{
    constructor( private usersService: UsersService )
    {
        super( initialState )
    }

    private readonly userProfileUnfilled$: Observable<string> = this.select( state => JSON.stringify( state.profileUnfilled, null, 4 ) )
    private readonly userInfo$: Observable<UserInfo | undefined> = this.select( state => state.userInfo )
    private readonly userInfoDocument$: Observable<Document> = this.select( state => state.userInfo?.document ?? this.getEmptyDocument() )
    private readonly userInfoDwelling$: Observable<Location> = this.select( state => state.userInfo?.dwelling ?? this.getEmptyLocation() )
    private readonly userInfoLimitations$: Observable<UserLimitations> = this.select( state => state.userInfo?.limitations ?? this.getEmptyLimitations() )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    // @ts-ignore
    readonly viewModel$: Observable<{
        loading: boolean; error: string | null, userProfileUnfilled: string,
        userInfo: UserInfo,
        userInfoDocument: Document,
        userInfoDwelling: Location,
        userInfoLimitations: UserLimitations,
    }> = this.select(
        this.loading$,
        this.error$,
        this.userProfileUnfilled$,
        this.userInfo$,
        this.userInfoDocument$,
        this.userInfoDwelling$,
        this.userInfoLimitations$,
        ( loading, error, userProfileUnfilled, userInfo, userInfoDocument, userInfoDwelling, userInfoLimitations ) => ( {
            loading: loading,
            error: error,
            userProfileUnfilled: userProfileUnfilled,
            userInfo: userInfo ?? {},
            userInfoDocument: userInfoDocument,
            userInfoDwelling: userInfoDwelling,
            userInfoLimitations: this.getLimitationsForViewModel( userInfoLimitations )
        } )
    )


    private getLimitationsForViewModel( userInfoLimitations: UserLimitations )
    {
        // @ts-ignore
        return { ...userInfoLimitations, user_id: undefined }
    }

    private getEmptyDocument(): Document
    {
        return {
            document_name: undefined,
            document_type: DocumentTypeEnum.RfPassport,
            issue_date: undefined,
            issuer: undefined,
            number: undefined,
            series: undefined,
            code: undefined,
            user_id: undefined
        }
    }

    private getEmptyLocation(): Location
    {
        return {
            country: "Россия",
            city: {
                region_name: "",
                name: ""
            },
            location_type: LocationTypeEnum.Russian,
            rural: false
        } as LocationRussia
    }

    private getEmptyLimitations(): UserLimitations
    {
        return {
            hearing: false,
            movement: false,
            sight: false,
            // @ts-ignore
            user_id: undefined
        }
    }

    // UPDATERS
    readonly updateError = this.updater( ( state: ProfileState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ProfileState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ProfileState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setUserInfo = this.updater( ( state: ProfileState, response: UserInfo ) =>
        ( {
            ...state, userInfo: response
        } )
    )

    readonly setProfileUnfilled = this.updater( ( state: ProfileState, response: any ) =>
        ( {
            ...state, profileUnfilled: response
        } )
    )

    // EFFECTS
    readonly fetch = this.effect( () =>
    {
        this.setLoading()
        return zip( [ this.fetchUserInfo, this.fetchUnfilled ] ).pipe(
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
            finalize( () => this.setLoaded )
        )
    } )


    readonly fetchUnfilled = this.effect( () =>
        this.usersService.userProfileUnfilledGet().pipe(
            tapResponse(
                ( response: any ) => this.setProfileUnfilled( response ),
                ( error: string ) => this.updateError( error )
            )
        ) )

    readonly fetchUserInfo = this.effect( () =>
        this.usersService.userProfilePersonalGet().pipe(
            tapResponse(
                ( response: UserInfo ) => this.setUserInfo( response ),
                ( error: string ) => this.updateError( error )
            )
        ) )


    readonly updateUserInfo = this.effect( ( userInfo$: Observable<UserInfo> ) =>
        userInfo$.pipe(
            withLatestFrom( this.userInfoDocument$, this.userInfoDwelling$, this.userInfoLimitations$ ),
            switchMap( ( [ userInfo, document, dwelling, limitations ] ) =>
            {
                this.setLoading()
                const newUserInfo = { ...userInfo }
                newUserInfo.document = document
                newUserInfo.dwelling = dwelling
                newUserInfo.limitations = limitations
                return this.usersService.userProfilePersonalPatch( newUserInfo ).pipe(
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                )
            } )
        ) )

}
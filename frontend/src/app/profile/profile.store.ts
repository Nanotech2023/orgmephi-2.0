import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import {
    Document,
    DocumentRF,
    LocationOther,
    LocationRussia,
    SchoolInfo,
    UserInfo,
    UserLimitations
} from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { EMPTY, Observable, zip } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { catchError, finalize, switchMap } from 'rxjs/operators'
import { DocumentTypeEnum } from '@api/users/models/documentType'


export interface ProfileState
{
    userInfo?: UserInfo
    schoolInfo: SchoolInfo | null
    profileUnfilled: any
    callState: CallState
}


const initialState: ProfileState = {
    userInfo: undefined,
    schoolInfo: null,
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

    readonly userProfileUnfilled$: Observable<string> = this.select( state => JSON.stringify( state.profileUnfilled, null, 4 ) )
    readonly userInfo$: Observable<UserInfo | undefined> = this.select( state => state.userInfo )
    readonly userInfoDocument$: Observable<DocumentRF | undefined> = this.select( state => state.userInfo?.document as DocumentRF )
    readonly userInfoDwelling$: Observable<LocationRussia | undefined> = this.select( state => state.userInfo?.dwelling as LocationRussia )
    readonly userInfoLimitations$: Observable<UserLimitations | undefined> = this.select( state => state.userInfo?.limitations )
    readonly schoolInfo$: Observable<SchoolInfo | null> = this.select( state => state.schoolInfo )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    readonly viewModel$: Observable<{
        loading: boolean; error: string | null, userProfileUnfilled: string,
        userInfo: UserInfo,
        userInfoDocument: DocumentRF,
        userInfoDwelling: LocationRussia,
        userInfoLimitations: UserLimitations,
        schoolInfo: SchoolInfo
    }> = this.select(
        this.loading$,
        this.error$,
        this.userProfileUnfilled$,
        this.userInfo$,
        this.userInfoDocument$,
        this.userInfoDwelling$,
        this.userInfoLimitations$,
        this.schoolInfo$,
        ( loading, error, userProfileUnfilled, userInfo, userInfoDocument, userInfoDwelling, userInfoLimitations, schoolInfo ) => ( {
            loading: loading,
            error: error,
            userProfileUnfilled: userProfileUnfilled,
            userInfo: userInfo ?? {},
            userInfoDocument: userInfoDocument ?? this.getEmptyDocument(),
            userInfoDwelling: userInfoDwelling ?? this.getEmptyLocation(),
            userInfoLimitations: userInfoLimitations ?? this.getEmptyLimitations(),
            schoolInfo: schoolInfo ?? this.getEmptySchool()
        } )
    )


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

    private getEmptyLocation(): LocationRussia
    {
        return {
            country: "Россия",
            city: {
                region_name: "",
                name: ""
            },
            location_type: LocationOther.LocationTypeEnum.Russian,
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

    getEmptySchool(): SchoolInfo
    {
        return {
            grade: undefined,
            number: undefined,
            user_id: undefined,
            school_type: SchoolInfo.SchoolTypeEnum.School,
            name: undefined,
            location: this.getEmptyLocation()
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

    readonly setSchoolInfo = this.updater( ( state: ProfileState, response: SchoolInfo ) =>
        ( {
            ...state, schoolInfo: response
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
        return zip( [ this.fetchUserInfo, this.fetchSchoolInfo, this.fetchUnfilled ] ).pipe(
            catchError( () => EMPTY ),
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

    readonly fetchSchoolInfo = this.effect( () =>
        this.usersService.userProfileSchoolGet().pipe(
            tapResponse(
                ( response: SchoolInfo ) => this.setSchoolInfo( response ),
                ( error: string ) => this.updateError( error )
            )
        ) )

    readonly updateUserInfo = this.effect( ( userInfo$: Observable<UserInfo> ) =>
        userInfo$.pipe(
            switchMap( ( userInfo: UserInfo ) =>
            {
                this.setLoading()
                return this.usersService.userProfilePersonalPatch( userInfo ).pipe(
                    catchError( () => EMPTY )
                )
            } )
        ) )

    readonly updateSchoolInfo = this.effect( ( userInfo$: Observable<SchoolInfo> ) =>
        userInfo$.pipe(
            switchMap( ( userInfo: SchoolInfo ) =>
            {
                this.setLoading()
                return this.usersService.userProfileSchoolPatch( userInfo ).pipe(
                    catchError( () => EMPTY )
                )
            } )
        ) )
}

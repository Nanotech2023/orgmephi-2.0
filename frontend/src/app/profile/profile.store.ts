import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { SchoolInfo, UserInfo } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { EMPTY, Observable, zip } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { catchError, finalize, switchMap } from 'rxjs/operators'


export interface ProfileState
{
    userInfo: UserInfo | null
    schoolInfo: SchoolInfo | null
    profileUnfilled: any
    callState: CallState
}


const initialState: ProfileState = {
    userInfo: null,
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
    readonly userInfo$: Observable<UserInfo | null> = this.select( state => state.userInfo )
    readonly schoolInfo$: Observable<UserInfo | null> = this.select( state => state.schoolInfo )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    readonly viewModel$: Observable<{ loading: boolean; error: string | null, userProfileUnfilled: string, userInfo: UserInfo, schoolInfo: SchoolInfo }> = this.select(
        this.loading$,
        this.error$,
        this.userProfileUnfilled$,
        this.userInfo$,
        this.schoolInfo$,
        ( loading, error, userProfileUnfilled, userInfo, schoolInfo ) => ( {
            loading: loading,
            error: error,
            userProfileUnfilled: userProfileUnfilled,
            userInfo: userInfo ?? {},
            schoolInfo: schoolInfo ?? {}
        } )
    )

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

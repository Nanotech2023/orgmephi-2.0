import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { SchoolInfo, UserInfo } from '@api/users/models'
import { CallState, LoadingState } from '@/shared/callState'
import { UsersService } from '@api/users/users.service'
import { Observable, of, zip } from 'rxjs'
import { ProfileState } from '@/profile/profile.store'
import { catchError, finalize, switchMap } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'


export interface ProfileSchoolState
{
    schoolInfo?: SchoolInfo
    profileUnfilled: any
    callState: CallState
}


const initialState: ProfileSchoolState = {
    schoolInfo: undefined,
    profileUnfilled: null,
    callState: LoadingState.INIT
}


@Injectable()
export class ProfileSchoolStore extends ComponentStore<ProfileSchoolState>
{
    constructor( private usersService: UsersService )
    {
        super( initialState )
    }

    private readonly userProfileUnfilled$: Observable<string> = this.select( state => JSON.stringify( state.profileUnfilled, null, 4 ) )
    readonly schoolInfo$: Observable<SchoolInfo> = this.select( state => state.schoolInfo ?? this.getEmptySchool() )

    private getEmptySchool(): SchoolInfo
    {
        return {}
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
        return zip( [ this.fetchSchoolInfo, this.fetchUnfilled ] ).pipe(
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
            finalize( () => this.setLoaded )
        )
    } )

    readonly fetchSchoolInfo = this.effect( () =>
        this.usersService.userProfileSchoolGet().pipe(
            tapResponse(
                ( response: SchoolInfo ) => this.setSchoolInfo( response ),
                ( error: string ) => this.updateError( error )
            )
        ) )

    readonly fetchUnfilled = this.effect( () =>
        this.usersService.userProfileUnfilledGet().pipe(
            tapResponse(
                ( response: any ) => this.setProfileUnfilled( response ),
                ( error: string ) => this.updateError( error )
            )
        ) )

    readonly updateSchoolInfo = this.effect( ( schoolInfo$: Observable<SchoolInfo> ) =>
        schoolInfo$.pipe(
            switchMap( ( schoolInfo: SchoolInfo ) =>
            {
                this.setLoading()
                const newSchoolInfo = { ...schoolInfo }
                return this.usersService.userProfileSchoolPatch( newSchoolInfo ).pipe(
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                )
            } )
        ) )
}

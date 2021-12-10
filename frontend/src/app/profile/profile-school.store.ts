import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import {
    Location,
    LocationRussia,
    LocationRussiaCity,
    LocationTypeEnum,
    SchoolInfo,
} from '@api/users/models'
import { CallState, getError, LoadingState } from '@/shared/callState'
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
    private readonly schoolInfo$: Observable<SchoolInfo> = this.select( state => state.schoolInfo ?? this.getEmptySchool() )
    private readonly schoolLocation$: Observable<Location> = this.select( state => state.schoolInfo?.location ?? this.getEmptyLocation() )
    private readonly schoolLocationCity$: Observable<LocationRussiaCity> = this.select( state => ( state.schoolInfo?.location as LocationRussia )?.city ?? this.getEmptyCity() )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )

    // @ts-ignore
    readonly viewModel$: Observable<{
        loading: boolean;
        error: string | null,
        userProfileUnfilled: string,
        schoolInfo: SchoolInfo,
        schoolLocation: Location,
        schoolLocationCity: LocationRussiaCity
    }> = this.select(
        this.loading$,
        this.error$,
        this.userProfileUnfilled$,
        this.schoolInfo$,
        this.schoolLocation$,
        this.schoolLocationCity$,
        ( loading, error, userProfileUnfilled, schoolInfo, schoolLocation, schoolLocationCity ) => ( {
            loading: loading,
            error: error,
            userProfileUnfilled: userProfileUnfilled,
            schoolInfo: schoolInfo ?? this.getEmptySchool(),
            schoolLocation: schoolLocation,
            schoolLocationCity: schoolLocationCity
        } )
    )

    private getEmptySchool(): SchoolInfo
    {
        return {}
    }


    private getEmptyCity(): LocationRussiaCity
    {
        return {
            region_name: "",
            name: ""
        }
    }

    private getEmptyLocation(): Location
    {
        return {
            country: "Россия",
            location_type: LocationTypeEnum.Russian,
            rural: false
        } as LocationRussia
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

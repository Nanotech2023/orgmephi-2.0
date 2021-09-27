import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { User, UserInfo } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { EMPTY, Observable } from 'rxjs'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { catchError, switchMap } from 'rxjs/operators'


export interface ProfileState
{
    userInfo: UserInfo | null
    callState: CallState
}


const initialState: ProfileState = {
    userInfo: null,
    callState: LoadingState.INIT
}


@Injectable()
export class ProfileStore extends ComponentStore<ProfileState>
{
    constructor( private usersService: UsersService )
    {
        super( initialState )
    }

    readonly userInfo$: Observable<UserInfo | null> = this.select( state => state.userInfo )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )


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

    // EFFECTS
    readonly fetch = this.effect( () =>
    {
        this.setLoading()
        return this.usersService.userProfilePersonalGet().pipe(
            tapResponse(
                ( response: UserInfo ) => this.setUserInfo( response ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )


    readonly update = this.effect( ( userInfo$: Observable<UserInfo> ) =>
        userInfo$.pipe(
            switchMap( ( userInfo: UserInfo ) =>
            {
                this.setLoading()
                return this.usersService.userProfilePersonalPatch( userInfo ).pipe(
                    catchError( () => EMPTY )
                )
            } )
        ) )
}

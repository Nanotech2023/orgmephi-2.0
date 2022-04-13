import { createReducer, on } from '@ngrx/store'
import {
    getUserInfoSuccess,
    getUserPhotoSuccess, getUserProfileUnfilledSuccess,
    getUserSuccess,
    loginSuccess,
    logoutSuccess
} from '@/auth/store/auth.actions'
import { CSRFPairUser, User, UserInfo } from '@api/users/models'


export const featureKey: string = 'auth'


export interface State
{
    csrfTokens: CSRFPairUser | null
    user: User | null,
    userInfo: UserInfo | null
    userPhoto: Blob | null
    unfilled: Array<object> | undefined
}


const initialState: State = {
    csrfTokens: null,
    user: null,
    userInfo: null,
    userPhoto: null,
    unfilled: undefined
}

export const reducer =
    createReducer(
        initialState,
        on( loginSuccess,
            ( state, { csrfPair } ) =>
            {
                localStorage.setItem( 'CSRFAccessToken', csrfPair.csrf_access_token )
                localStorage.setItem( 'CSRFRefreshToken', csrfPair.csrf_refresh_token )
                return ( { ...state, csrfTokens: csrfPair } )
            }
        ),
        on( logoutSuccess,
            ( state ) =>
            {
                localStorage.removeItem( 'CSRFAccessToken' )
                localStorage.removeItem( 'CSRFRefreshToken' )
                return ( { ...state, csrfTokens: null } )
            }
        ),
        on( getUserSuccess,
            ( state, { user } ) =>
                ( { ...state, user: user } )
        ),
        on( getUserInfoSuccess,
            ( state, { userInfo } ) =>
                ( { ...state, userInfo: userInfo } )
        ),
        on( getUserProfileUnfilledSuccess,
            ( state, { unfilled } ) =>
                ( { ...state, unfilled: unfilled } )
        ),
        on( getUserPhotoSuccess,
            ( state, { userPhoto } ) =>
                ( { ...state, userPhoto: userPhoto } )
        )
    )
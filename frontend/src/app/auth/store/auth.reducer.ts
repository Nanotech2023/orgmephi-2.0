import { createReducer, on } from '@ngrx/store'
import { getUserInfoSuccess, getUserSuccess, loginSuccess } from '@/auth/store/auth.actions'
import { CSRFPairUser, User, UserInfo } from '@api/users/models'


export const featureKey: string = 'auth'


export interface State
{
    csrfTokens: CSRFPairUser | null
    user: User | null,
    userInfo: UserInfo | null
}


const initialState: State = {
    csrfTokens: null,
    user: null,
    userInfo: null
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
        on( getUserSuccess,
            ( state, { user } ) =>
                ( { ...state, user: user } )
        ),
        on( getUserInfoSuccess,
            ( state, { userInfo } ) =>
                ( { ...state, userInfo: userInfo } )
        )
    )
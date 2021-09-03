import { createReducer, on } from '@ngrx/store'
import { getUserInfoSuccess, getUserSuccess, loginSuccess } from '@/auth/store/auth.actions'
import { CSRFPairUser, User, UserInfo } from '@/auth/api/models'


export const featureKey: string = 'auth'


export interface State
{
    csrfTokens: CSRFPairUser | null
    user: User | null
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
                ( { ...state, csrfTokens: csrfPair } )
        ),
        on( getUserSuccess,
            ( state, { user } ) =>
                ( { ...state, user: user } )
        ),
        on( getUserInfoSuccess,
            ( state, { userInfo } ) =>
                ( { ...state, userInfo: userInfo } ) )
    )
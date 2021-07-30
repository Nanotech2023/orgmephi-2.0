import { createReducer, on } from '@ngrx/store'
import {
    loginAttempt,
    loginError,
    loginSuccess,
    pushPersonalInfo,
    registerAttempt,
    registerError,
    registerSuccess
} from '@/auth/store/auth.actions'
import { ErrorValue, TypeCSRFPair, TypePersonalInfo, TypeUserInfo } from '@/auth/models'


export const featureKey: string = 'auth'


export interface State
{
    csrfTokens: TypeCSRFPair | null
    userInfo: TypeUserInfo | null
    personalInfo: TypePersonalInfo | null
    errors: ErrorValue[] | null
}


export const initialState: State = {
    csrfTokens: null,
    userInfo: null,
    personalInfo: null,
    errors: null
}

export const reducer =
    createReducer(
        initialState,
        on( loginAttempt, registerAttempt,
            ( state ) =>
                ( { ...state } )
        ),
        on( loginSuccess,
            ( state, { responseLogin } ) =>
                ( { ...state, csrfTokens: { csrfAccessToken: '', csrfRefreshToken: '' } } ) // TODO tokens in responseLogin?
        ),
        on( registerSuccess,
            ( state, { responseRegistration } ) =>
                ( { ...state, userInfo: responseRegistration } ) // TODO remove assign userInfo
        ),
        on( loginError, registerError,
            ( state, { error } ) =>
                ( { ...state, error: error.errors } )
        ),
        on( pushPersonalInfo,
            ( state, { personalInfo } ) =>
                ( { ...state, personalInfo: personalInfo } ) // TODO this is mock action. Should be removed on production
        )
    )
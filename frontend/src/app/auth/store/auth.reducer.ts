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
import { AuthResponse, CommonUserInfo, PersonalInfo } from '@/auth/models'


export const featureKey: string = 'auth'


export interface State
{
    apiKeys: AuthResponse | null
    commonUserInfo: CommonUserInfo | null
    personalInfo: PersonalInfo | null
    error: string | null
}


export const initialState: State = {
    apiKeys: null,
    commonUserInfo: null,
    personalInfo: null,
    error: null
}

export const reducer =
    createReducer(
        initialState,
        on( loginAttempt, registerAttempt,
            ( state ) =>
                ( { ...state } )
        ),
        on( loginSuccess,
            ( state, { authResponse } ) =>
                ( { ...state, apiKeys: authResponse } )
        ),
        on( registerSuccess,
            ( state, { commonUserInfo } ) =>
                ( { ...state, commonUserInfo: commonUserInfo } )
        ),
        on( loginError, registerError,
            ( state, { error } ) =>
                ( { ...state, error: error.errorMsg } )
        ),
        on( pushPersonalInfo,
            ( state, { personalInfo } ) =>
                ( { ...state, personalInfo: personalInfo } )
        )
    )
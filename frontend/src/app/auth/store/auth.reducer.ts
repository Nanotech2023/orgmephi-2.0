import { createReducer, on } from '@ngrx/store'
import {
    error,
    getPersonalInfoSuccess,
    getUserInfoSuccess,
    loginSuccess,
    registerSuccess
} from '@/auth/store/auth.actions'
import { ErrorValue, TypeCSRFPair, TypePersonalInfo, TypeUserInfo } from '@/auth/api/models'


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
        on( loginSuccess,
            ( state, { csrfPair } ) =>
                ( { ...state, csrfTokens: csrfPair } )
        ),
        on( registerSuccess,
            ( state, { userInfo } ) =>
                ( { ...state, userInfo: userInfo } )
        ),
        on( getUserInfoSuccess,
            ( state, { userInfo } ) =>
                ( { ...state, userInfo: userInfo } ) ),
        on( getPersonalInfoSuccess,
            ( state, { personalInfo } ) =>
                ( { ...state, personalInfo: personalInfo } ) ),
        on( error,
            ( state, { error } ) =>
                ( { ...state, error: error.errors } )
        )
    )
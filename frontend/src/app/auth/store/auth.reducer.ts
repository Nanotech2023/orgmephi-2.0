import { createReducer, on } from '@ngrx/store'
import {
    getUserInfoSuccess,
    loginSuccess,
    registerSuccess
} from '@/auth/store/auth.actions'
import { ErrorValue, CSRFPairUser, User } from '@/auth/api/models'


export const featureKey: string = 'auth'


export interface State
{
    csrfTokens: CSRFPairUser | null
    user: User | null
    // personalInfo: TypePersonalInfo | null
    errors: ErrorValue[] | null
}


export const initialState: State = {
    csrfTokens: null,
    user: null,
    // personalInfo: null,
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
            ( state, { user } ) =>
                ( { ...state, user: user } )
        ),
        on( getUserInfoSuccess,
            ( state, { user } ) =>
                ( { ...state, user: user } ) ),
        // on( getPersonalInfoSuccess,
        //     ( state, { personalInfo } ) =>
        //         ( { ...state, personalInfo: personalInfo } ) ),
    )
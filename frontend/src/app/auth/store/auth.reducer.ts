import { AuthResult, RegisterResult, UserAuth, UserRegister } from '@/auth/models'
import { createReducer, on } from '@ngrx/store'
import {
    loginAttempt,
    loginError,
    loginSuccess,
    registerAttempt,
    registerError,
    registerSuccess
} from '@/auth/store/auth.actions'


export const featureKey: string = 'auth'


export interface State
{
    user: UserAuth | null
    registration: UserRegister
    authResult: AuthResult
    registrationResult: RegisterResult
}


export const initialState: State = {
    user: null,
    registration: {
        registerNumber: 'test',
        activationCode: 'test',
        email: 'test@test',
        password: '',
        name: 'test1',
        lastName: 'tes2',
        birthDate: new Date(),
        surname: ''
    },
    registrationResult: {
        isSuccessful: false,
        error: ''
    },
    authResult: {
        isSuccessful: true,
        error: ''
    }
}

export const reducer =
    createReducer(
        initialState,
        on( loginAttempt,
            ( state ) =>
            {
                const successAuthResult = { isSuccessful: false, error: '' }
                return ( { ...state, user: null, authResult: successAuthResult } )
            }
        ),
        on( loginSuccess,
            ( state, { user } ) =>
            {
                const errorAuthResult = { isSuccessful: true, error: '' }
                return ( { ...state, user: user, authResult: errorAuthResult } )
            }
        ),
        on( loginError,
            ( state, { result: authResult } ) =>
            {
                return ( { ...state, authResult: authResult } )
            }
        ),

        on( registerAttempt,
            ( state, { registration } ) =>
                ( { ...state, registration: registration } )
        ),
        on( registerSuccess,
            ( state, { registration } ) =>
            {
                const registrationResult = { isSuccessful: true, error: '' }
                return ( { ...state, registration: registration, registrationResult: registrationResult } )
            }
        ),
        on( registerError,
            ( state, { result } ) =>
                ( { ...state, registrationResult: result } )
        )
    )
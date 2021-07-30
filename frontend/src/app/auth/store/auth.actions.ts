import { createAction, props } from '@ngrx/store'
import {
    ErrorResponse,
    RequestLogin,
    RequestRegistration, TypeCSRFPair,
    TypeRegistrationPersonalInfo, TypeUserInfo
} from '@/auth/api/models'


export const loginAttempt = createAction(
    '[Auth] Login Attempt',
    props<{ requestLogin: RequestLogin }>()
)

export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ csrfPair: TypeCSRFPair }>()
)

export const loginError = createAction(
    '[Auth] Login Error',
    props<{ error: ErrorResponse }>()
)

export const registerAttempt = createAction(
    '[Auth] Register Attempt',
    props<{ requestRegistration: RequestRegistration }>()
)

export const registerSuccess = createAction(
    '[Auth] Register Success',
    props<{ userInfo: TypeUserInfo }>()
)

export const registerError = createAction(
    '[Auth] Register Error',
    props<{ error: ErrorResponse }>()
)

export const pushPersonalInfo = createAction(
    '[Auth] Push Personal Info',
    props<{ personalInfo: TypeRegistrationPersonalInfo }>()
)
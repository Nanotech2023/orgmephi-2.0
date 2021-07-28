import { createAction, props } from '@ngrx/store'
import { Authentication, AuthResponse, CommonUserInfo, ErrorResponse, PersonalInfo, Registration } from '@/auth/models'


export const loginAttempt = createAction(
    '[Auth] Login Attempt',
    props<{ authentication: Authentication }>()
)

export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ authResponse: AuthResponse }>()
)

export const loginError = createAction(
    '[Auth] Login Error',
    props<{ error: ErrorResponse }>()
)

export const registerAttempt = createAction(
    '[Auth] Register Attempt',
    props<{ registration: Registration }>()
)

export const registerSuccess = createAction(
    '[Auth] Register Success',
    props<{ commonUserInfo: CommonUserInfo }>()
)

export const registerError = createAction(
    '[Auth] Register Error',
    props<{ error: ErrorResponse }>()
)

export const pushPersonalInfo = createAction(
    '[Auth] Push Personal Info',
    props<{ personalInfo: PersonalInfo }>()
)
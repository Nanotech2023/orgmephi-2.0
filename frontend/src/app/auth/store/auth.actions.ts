import { createAction, props } from '@ngrx/store'
import { AuthResult, RegisterResult, UserAuth, UserRegister } from '@/auth/models'


export const loginAttempt = createAction(
    '[Auth] Login Attempt',
    props<{ user: UserAuth }>()
)

export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ user: UserAuth }>()
)

export const loginError = createAction(
    '[Auth] Login Error',
    props<{ result: AuthResult }>()
)

export const registerAttempt = createAction(
    '[Auth] Register Attempt',
    props<{ registration: UserRegister }>()
)

export const registerSuccess = createAction(
    '[Auth] Register Success',
    props<{ registration: UserRegister }>()
)

export const registerError = createAction(
    '[Auth] Register Error',
    props<{ result: RegisterResult }>()
)

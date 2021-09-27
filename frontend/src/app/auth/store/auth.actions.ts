import { createAction, props } from '@ngrx/store'
import { CSRFPairUser, LoginRequestUser, SchoolRegistrationRequestUser, User, UserInfo } from '@api/users/models'


export const loginRequest = createAction(
    '[Auth] Login Request',
    props<{ loginRequestUser: LoginRequestUser }>()
)
export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ csrfPair: CSRFPairUser }>()
)


export const registerRequest = createAction(
    '[Auth] Register Request',
    props<{ registrationRequestUser: SchoolRegistrationRequestUser }>()
)
export const registerSuccess = createAction(
    '[Auth] Register Success'
)


export const getUserRequest = createAction(
    '[Auth] Get User Request'
)
export const getUserSuccess = createAction(
    '[Auth] Get User Success',
    props<{ user: User }>()
)
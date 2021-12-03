import { createAction, props } from '@ngrx/store'
import { CSRFPairUser, LoginRequestUser, SchoolRegistrationRequestUser, User, UserInfo } from '@api/users/models'
import { ErrorMessage } from '@/shared/logging/errorMessage'


export const loginRequest = createAction(
    '[Auth] Login Request',
    props<{ loginRequestUser: LoginRequestUser }>()
)
export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ csrfPair: CSRFPairUser }>()
)


export const logoutRequest = createAction(
    '[Auth] Logout Request'
)
export const logoutSuccess = createAction(
    '[Auth] Logout Success'
)


export const registerRequest = createAction(
    '[Auth] Register Request',
    props<{ registrationRequestUser: SchoolRegistrationRequestUser }>()
)
export const registerSuccess = createAction(
    '[Auth] Register Success'
)


export const getUserPhotoRequest = createAction(
    '[Auth] Get User Photo Request'
)
export const getUserPhotoSuccess = createAction(
    '[Auth] Get User Photo Success',
    props<{ userPhoto: Blob }>()
)


export const getUserRequest = createAction(
    '[Auth] Get User Request'
)
export const getUserSuccess = createAction(
    '[Auth] Get User Success',
    props<{ user: User }>()
)


export const getUserInfoRequest = createAction(
    '[Auth] Get User Info Request'
)
export const getUserInfoSuccess = createAction(
    '[Auth] Get User Success',
    props<{ userInfo: UserInfo }>()
)


export const errorCaught = createAction(
    '[Auth] Error Caught',
    props<{ error: ErrorMessage }>()
)
import { createAction, props } from '@ngrx/store'
import {
    ErrorResponse,
    RequestLogin,
    RequestRegistrationSchool,
    TypeCSRFPair,
    TypePersonalInfo,
    TypeUserInfo
} from '@/auth/api/models'


export const loginRequest = createAction(
    '[Auth] Login Attempt',
    props<{ requestLogin: RequestLogin }>()
)
export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ csrfPair: TypeCSRFPair }>()
)


export const registerRequest = createAction(
    '[Auth] Register Attempt',
    props<{ requestRegistration: RequestRegistrationSchool }>()
)
export const registerSuccess = createAction(
    '[Auth] Register Success',
    props<{ userInfo: TypeUserInfo }>()
)


export const getUserInfoRequest = createAction(
    '[Auth] Get UserInfo Request'
)
export const getUserInfoSuccess = createAction(
    '[Auth] Get UserInfo Success',
    props<{ userInfo: TypeUserInfo }>()
)


export const getPersonalInfoRequest = createAction(
    '[Auth] Get PersonalInfo Request'
)
export const getPersonalInfoSuccess = createAction(
    '[Auth] Get PersonalInfo Success',
    props<{ personalInfo: TypePersonalInfo }>()
)


export const error = createAction(
    '[Auth] Error',
    props<{ error: ErrorResponse }>()
)
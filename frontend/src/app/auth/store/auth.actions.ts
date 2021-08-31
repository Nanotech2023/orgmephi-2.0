import { createAction, props } from '@ngrx/store'
import {
    LoginRequestUser,
    SchoolRegistrationRequestUser,
    CSRFPairUser,
    User
} from '@/auth/api/models'


export const loginRequest = createAction(
    '[Auth] Login Attempt',
    props<{ loginRequestUser: LoginRequestUser }>()
)
export const loginSuccess = createAction(
    '[Auth] Login Success',
    props<{ csrfPair: CSRFPairUser }>()
)


export const registerRequest = createAction(
    '[Auth] Register Attempt',
    props<{ registrationRequestUser: SchoolRegistrationRequestUser }>()
)
export const registerSuccess = createAction(
    '[Auth] Register Success',
    props<{ user: User }>()
)


export const getUserInfoRequest = createAction(
    '[Auth] Get User Request'
)
export const getUserInfoSuccess = createAction(
    '[Auth] Get User Success',
    props<{ user: User }>()
)


// export const getPersonalInfoRequest = createAction(
//     '[Auth] Get PersonalInfo Request'
// )
// export const getPersonalInfoSuccess = createAction(
//     '[Auth] Get PersonalInfo Success',
//     props<{ personalInfo: TypePersonalInfo }>()
// )
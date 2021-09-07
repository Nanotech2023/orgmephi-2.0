import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import { CSRFPairUser, DocumentInput, User, UserInfo, UserInfoRestrictedInput } from '@/auth/api/models'


export const selectFeature: MemoizedSelector<object, State> = createFeatureSelector<State>( featureKey )

export const selectApiKeys: MemoizedSelector<State, CSRFPairUser> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens!
)

export const selectIsAuthorized: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.csrfTokens !== null
)

export const selectUser: MemoizedSelector<State, User> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user!
)
export const selectUserInfo: MemoizedSelector<State, UserInfo> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.userInfo!
)

export const selectIsParticipant: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user?.role === User.RoleEnum.Participant
)

export const selectAccessToManagePages: MemoizedSelector<State, boolean> = createSelector(
    selectFeature,
    ( state: State ) =>
        state.user?.role === User.RoleEnum.Creator || state.user?.role === User.RoleEnum.Admin || state.user?.role === User.RoleEnum.System
)

export const copy: MemoizedSelector<State, UserInfoRestrictedInput> = createSelector(
    selectFeature,
    ( state: State ) =>
    {
        const userInfo: UserInfo = state.userInfo!

        const document = userInfo.document!
        let y: DocumentInput = ( {
            code: document.code || undefined,
            document_type: userInfo.document!.document_type || undefined, // !
            issue_date: userInfo.document!.issue_date || undefined,
            issuer: userInfo.document!.issuer || undefined,
            number: userInfo.document!.number || undefined,
            series: userInfo.document!.series || undefined,
            document_name: userInfo.document!.document_name || undefined
        } )
        const newVar1 = userInfo.dwelling!
        const newVar3 = { country: newVar1.country, location: newVar1.russian ?? "", rural: newVar1.rural ?? false }

        const gender = userInfo.gender

        const limitations = userInfo?.limitations
        const newVar2 = {
            hearing: limitations?.hearing || undefined,
            movement: limitations?.movement || undefined,
            sight: limitations?.sight || undefined
        }

        const placeOfBirth = userInfo?.place_of_birth || undefined

        const newVar: UserInfoRestrictedInput = {
            document: y,
            dwelling: newVar3,
            gender: gender, // !
            limitations: newVar2,
            place_of_birth: placeOfBirth
        }
        return newVar
    }
)
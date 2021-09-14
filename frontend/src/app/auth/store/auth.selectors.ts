import { createFeatureSelector, createSelector, MemoizedSelector } from '@ngrx/store'
import { featureKey, State } from '@/auth/store/auth.reducer'
import {
    CSRFPairUser,
    Document,
    DocumentInput, DocumentTypeEnum,
    GenderEnum,
    Location,
    LocationInput,
    User,
    UserInfo,
    UserInfoRestrictedInput,
    UserLimitations,
    UserLimitationsInput
} from '@api/users/models'


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

        const document: Document | null = userInfo.document!
        const documentInput: DocumentInput = ( {
            code: document.code || undefined,
            document_type: userInfo.document!.document_type || DocumentTypeEnum.RfPassport,
            issue_date: userInfo.document!.issue_date || undefined,
            issuer: userInfo.document!.issuer || undefined,
            number: userInfo.document!.number || undefined,
            series: userInfo.document!.series || undefined,
            document_name: userInfo.document!.document_name || undefined
        } )
        const dwelling: Location = userInfo.dwelling!
        const dwellingInput: LocationInput = {
            country: dwelling.country,
            location: dwelling.russian ?? "",
            rural: dwelling.rural ?? false
        }

        const genderInput: GenderEnum | undefined = userInfo.gender || undefined

        const limitations: UserLimitations | undefined = userInfo?.limitations || undefined
        const limitationInput: UserLimitationsInput = {
            hearing: limitations?.hearing || undefined,
            movement: limitations?.movement || undefined,
            sight: limitations?.sight || undefined
        }

        const placeOfBirthInput: string | undefined = userInfo?.place_of_birth || undefined
        const phoneInput: string | undefined = userInfo?.phone || undefined

        const result: UserInfoRestrictedInput = {
            document: documentInput,
            dwelling: dwellingInput,
            gender: genderInput,
            limitations: limitationInput,
            place_of_birth: placeOfBirthInput,
            phone: phoneInput
        }
        return result
    }
)
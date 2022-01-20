import { Component, forwardRef } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import { Document, GenderEnum, Location, LocationRussiaCity, UserInfo, UserLimitations } from '@api/users/models'
import { getGenderDisplay } from '@/shared/localizeUtils'
import { NG_VALIDATORS } from '@angular/forms'
import { PhoneValidatorDirective } from '@/shared/validators/phone.validator.directive'


@Component( {
    selector: 'app-profile-edit-userinfo',
    templateUrl: './profile-edit-userinfo.component.html',
    styleUrls: [ './profile-edit-userinfo.component.scss' ],
    providers: [
        ProfileStore,
        { provide: NG_VALIDATORS, useExisting: forwardRef( () => PhoneValidatorDirective ), multi: true }
    ]
} )
export class ProfileEditUserinfoComponent
{
    viewModel$: Observable<{
        loading: boolean; error: string | null, userProfileUnfilled: string,
        userInfo: UserInfo,
        userInfoDocument: Document,
        userInfoDwelling: any,
        userInfoDwellingCity: LocationRussiaCity,
        userInfoLimitations: UserLimitations,
    }>

    readonly genders: GenderEnum[] = [ GenderEnum.Male, GenderEnum.Female ]

    constructor( private profileStore: ProfileStore )
    {
        this.profileStore.fetch()
        this.viewModel$ = this.profileStore.viewModel$
    }

    getGenderDisplay( genderEnum: GenderEnum ): string
    {
        return getGenderDisplay( genderEnum )
    }

    onSubmit( userInfo: UserInfo ): void
    {
        this.profileStore.updateUserInfo( userInfo )
    }
}
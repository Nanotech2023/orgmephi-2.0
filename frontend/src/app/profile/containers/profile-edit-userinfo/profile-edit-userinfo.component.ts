import { Component, forwardRef } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import { Document, GenderEnum, Location, LocationRussiaCity, UserInfo, UserLimitations } from '@api/users/models'
import { getGenderDisplay } from '@/shared/displayUtils'
import { NG_VALIDATORS } from '@angular/forms'
import { PhoneValidatorDirective } from '@/shared/phone.validator.directive'
import { Router } from '@angular/router'


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
        userInfoDwelling: Location,
        userInfoDwellingCity: LocationRussiaCity,
        userInfoLimitations: UserLimitations,
    }>

    readonly genders: GenderEnum[] = [ GenderEnum.Male, GenderEnum.Female ]

    constructor( private profileStore: ProfileStore, private router: Router )
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

    onCityChange( $event: LocationRussiaCity )
    {
        this.profileStore.setCity( $event )
    }
}
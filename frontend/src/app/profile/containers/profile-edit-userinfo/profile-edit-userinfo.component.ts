import { Component, forwardRef, OnInit } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import {
    Document,
    DocumentRF,
    GenderEnum, Location,
    LocationRussia, LocationRussiaCity,
    SchoolInfo,
    UserInfo,
    UserLimitations
} from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { getGenderDisplay } from '@/shared/displayUtils'
import { Router } from '@angular/router'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { NG_VALIDATORS } from '@angular/forms'
import { PhoneValidatorDirective } from '@/shared/phone.validator.directive'


@Component( {
    selector: 'app-profile-edit-userinfo',
    templateUrl: './profile-edit-userinfo.component.html',
    styleUrls: [ './profile-edit-userinfo.component.scss' ],
    providers: [
        ProfileStore,
        { provide: NG_VALIDATORS, useExisting: forwardRef( () => PhoneValidatorDirective ), multi: true }
    ]
} )
export class ProfileEditUserinfoComponent implements OnInit
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
    isPrivileged$!: Observable<boolean>

    constructor( private profileStore: ProfileStore, private router: Router, private usersService: UsersService, private store: Store<AuthState.State> )
    {
        this.profileStore.fetch()
        this.viewModel$ = this.profileStore.viewModel$
    }

    ngOnInit(): void
    {
        this.isPrivileged$ = this.store.select( AuthSelectors.selectIsPrivileged )
    }

    updateUserInfo( userInfo: UserInfo ): void
    {
        this.profileStore.updateUserInfo( userInfo )
        this.profileStore.fetch()
    }

    getGenderDisplay( genderEnum: GenderEnum ): string
    {
        return getGenderDisplay( genderEnum )
    }

    logoutButtonClick(): void
    {
        this.store.dispatch( AuthActions.logoutRequest() )
    }

    onSubmit( userInfo: UserInfo )
    {
        this.updateUserInfo( userInfo )
    }

    onCityChange( $event: LocationRussiaCity )
    {
        this.profileStore.setCity( $event )
    }
}
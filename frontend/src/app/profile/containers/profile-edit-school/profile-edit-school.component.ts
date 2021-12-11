import { Component, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { Location, LocationRussiaCity, SchoolInfo, SchoolTypeEnum } from '@api/users/models'
import { Router } from '@angular/router'
import { UsersService } from '@api/users/users.service'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { getSchoolTypeDisplay } from '@/shared/displayUtils'
import { ProfileSchoolStore } from '@/profile/profile-school.store'


@Component( {
    selector: 'app-profile-edit-school',
    templateUrl: './profile-edit-school.component.html',
    styleUrls: [ './profile-edit-school.component.scss' ],
    providers: [ ProfileSchoolStore ]
} )
export class ProfileEditSchoolComponent implements OnInit
{
    isPrivileged$!: Observable<boolean>

    viewModel$: Observable<{
        loading: boolean;
        error: string | null,
        userProfileUnfilled: string,
        schoolInfo: SchoolInfo,
        schoolLocation: Location,
        schoolLocationCity: LocationRussiaCity
    }>

    schoolTypes: SchoolTypeEnum[] = [
        SchoolTypeEnum.School,
        SchoolTypeEnum.Lyceum,
        SchoolTypeEnum.Gymnasium,
        SchoolTypeEnum.EducationCenter,
        SchoolTypeEnum.NightSchool,
        SchoolTypeEnum.External,
        SchoolTypeEnum.Collage,
        SchoolTypeEnum.University,
        SchoolTypeEnum.Correctional,
        SchoolTypeEnum.Other
    ]

    constructor( private profileStore: ProfileSchoolStore, private router: Router, private usersService: UsersService, private store: Store<AuthState.State> )
    {
        this.profileStore.fetch()
        this.viewModel$ = this.profileStore.viewModel$
    }

    ngOnInit(): void
    {
        this.isPrivileged$ = this.store.select( AuthSelectors.selectIsPrivileged )
    }

    updateSchoolInfo( schoolInfo: SchoolInfo ): void
    {
        this.profileStore.updateSchoolInfo( schoolInfo )
    }

    logoutButtonClick(): void
    {
        this.store.dispatch( AuthActions.logoutRequest() )
    }

    onSubmit( schoolInfo: { loading: boolean; error: string | null; userProfileUnfilled: string; schoolInfo: SchoolInfo; schoolLocation: Location; schoolLocationCity: LocationRussiaCity } )
    {
        this.updateSchoolInfo( schoolInfo.schoolInfo )
    }

    getSchoolTypeDisplay( schoolType: SchoolTypeEnum ): string
    {
        return getSchoolTypeDisplay( schoolType )
    }

    onCityChange( $event: LocationRussiaCity )
    {
        this.profileStore.setCity( $event )
    }
}

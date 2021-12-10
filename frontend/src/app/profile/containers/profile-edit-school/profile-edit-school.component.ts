import { Component, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { SchoolInfo, SchoolTypeEnum } from '@api/users/models'
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
    viewModel$: Observable<SchoolInfo>

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
        this.viewModel$ = this.profileStore.schoolInfo$
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

    onSubmit( schoolInfo: SchoolInfo )
    {
        this.updateSchoolInfo( schoolInfo )
    }


    getSchoolTypeDisplay( schoolType: SchoolTypeEnum ): string
    {
        return getSchoolTypeDisplay( schoolType )
    }
}

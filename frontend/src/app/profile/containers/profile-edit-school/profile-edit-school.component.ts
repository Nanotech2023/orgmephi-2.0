import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Observable } from 'rxjs'
import { LocationRussia, SchoolInfo, SchoolTypeEnum } from '@api/users/models'
import { ProfileStore } from '@/profile/profile.store'
import { Router } from '@angular/router'
import { UsersService } from '@api/users/users.service'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { getSchoolTypeDisplay } from '@/shared/displayUtils'


@Component( {
    selector: 'app-profile-edit-school',
    templateUrl: './profile-edit-school.component.html',
    styleUrls: [ './profile-edit-school.component.scss' ],
    providers: [ ProfileStore ]
} )
export class ProfileEditSchoolComponent
{
    isPrivileged$!: Observable<boolean>
    viewModel$: Observable<SchoolInfo>

    constructor( private profileStore: ProfileStore, private router: Router, private usersService: UsersService, private store: Store<AuthState.State> )
    {
        this.profileStore.fetch2()
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

    @Input() model!: SchoolInfo
    @Output() modelChange = new EventEmitter<SchoolInfo>()
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

    get schoolLocation(): LocationRussia
    {
        return this.model.location as LocationRussia
    }

    set schoolLocation( location: LocationRussia )
    {
        this.model.location = location
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }

    getSchoolTypeDisplay( schoolType: SchoolTypeEnum ): string
    {
        return getSchoolTypeDisplay( schoolType )
    }
}

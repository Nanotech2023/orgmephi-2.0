import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { Location, LocationRussiaCity, SchoolInfo, SchoolTypeEnum } from '@api/users/models'
import { getSchoolTypeDisplay } from '@/shared/localizeUtils'
import { ProfileSchoolStore } from '@/profile/profile-school.store'


@Component( {
    selector: 'app-profile-edit-school',
    templateUrl: './profile-edit-school.component.html',
    styleUrls: [ './profile-edit-school.component.scss' ],
    providers: [ ProfileSchoolStore ]
} )
export class ProfileEditSchoolComponent
{
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
        SchoolTypeEnum.Correctional
    ]

    constructor( private profileStore: ProfileSchoolStore )
    {
        this.profileStore.fetch()
        this.viewModel$ = this.profileStore.viewModel$
    }

    onSubmit( schoolInfo: { loading: boolean; error: string | null; userProfileUnfilled: string; schoolInfo: SchoolInfo; schoolLocation: Location; schoolLocationCity: LocationRussiaCity } ): void
    {
        this.profileStore.updateSchoolInfo( schoolInfo.schoolInfo )
    }

    getSchoolTypeDisplay( schoolType: SchoolTypeEnum ): string
    {
        return getSchoolTypeDisplay( schoolType )
    }

    onCityChange( $event: LocationRussiaCity ): void
    {
        this.profileStore.setCity( $event )
    }
}

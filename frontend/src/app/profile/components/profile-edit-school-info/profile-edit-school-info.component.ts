import { getSchoolTypeDisplay } from '@/shared/displayUtils'
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { LocationRussia, SchoolInfo, SchoolTypeEnum } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-school-info',
    templateUrl: './profile-edit-school-info.component.html',
    styleUrls: [ './profile-edit-school-info.component.scss' ]
} )
export class ProfileEditSchoolInfoComponent
{
    // @Input() model!: SchoolInfo
    // @Output() modelChange = new EventEmitter<SchoolInfo>()
    // schoolTypes: SchoolTypeEnum[] = [
    //     SchoolTypeEnum.School,
    //     SchoolTypeEnum.Lyceum,
    //     SchoolTypeEnum.Gymnasium,
    //     SchoolTypeEnum.EducationCenter,
    //     SchoolTypeEnum.NightSchool,
    //     SchoolTypeEnum.Technical,
    //     SchoolTypeEnum.External,
    //     SchoolTypeEnum.Collage,
    //     SchoolTypeEnum.ProfTech,
    //     SchoolTypeEnum.University,
    //     SchoolTypeEnum.Correctional,
    //     SchoolTypeEnum.Other
    // ]
    //
    //
    // get schoolLocation(): LocationRussia
    // {
    //     return this.model.location as LocationRussia
    // }
    //
    // set schoolLocation( location: LocationRussia )
    // {
    //     this.model.location = location
    // }
    //
    // onModelChange(): void
    // {
    //     this.modelChange.emit( this.model )
    // }
    //
    // getSchoolTypeDisplay( schoolType: SchoolTypeEnum ): string
    // {
    //     return getSchoolTypeDisplay(schoolType)
    // }
}

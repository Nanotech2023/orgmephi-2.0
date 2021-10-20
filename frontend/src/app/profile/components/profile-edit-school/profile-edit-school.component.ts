import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { SchoolInfo } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-school',
    templateUrl: './profile-edit-school.component.html',
    styleUrls: [ './profile-edit-school.component.scss' ]
} )
export class ProfileEditSchoolComponent implements OnInit
{
    @Input() model!: SchoolInfo | undefined
    @Output() modelChange = new EventEmitter<SchoolInfo>()
    schoolInfo! : SchoolInfo

    ngOnInit(): void
    {
        this.schoolInfo = this.model ?? this.getEmptySchool()
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.schoolInfo )
    }

    getEmptySchool(): SchoolInfo
    {
        return {
            grade: undefined,
            number: undefined,
            user_id: undefined,
            school_type: SchoolInfo.SchoolTypeEnum.School,
            name: undefined
        }
    }
}

import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { UserLimitations } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-limitations',
    templateUrl: './profile-edit-limitations.component.html',
    styleUrls: [ './profile-edit-limitations.component.scss' ]
} )
export class ProfileEditLimitationsComponent implements OnInit
{
    @Input() model!: UserLimitations | undefined
    @Output() modelChange = new EventEmitter<UserLimitations>()
    limitations!: UserLimitations

    ngOnInit(): void
    {
        this.limitations = this.model!
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.limitations )
    }
}
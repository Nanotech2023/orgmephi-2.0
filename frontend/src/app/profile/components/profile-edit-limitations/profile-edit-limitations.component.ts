import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Document, Location, LocationOther, UserLimitations } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-limitations',
    templateUrl: './profile-edit-limitations.component.html',
    styleUrls: [ './profile-edit-limitations.component.scss' ]
} )
export class ProfileEditLimitationsComponent
{
    @Input() model!: UserLimitations | undefined
    @Output() modelChange = new EventEmitter<UserLimitations>()
    limitations: UserLimitations = this.model ?? this.getEmptyLimitations()

    onModelChange(): void
    {
        this.modelChange.emit( this.limitations )
    }

    private getEmptyLimitations(): UserLimitations
    {
        return {
            hearing: undefined,
            movement: undefined,
            sight: undefined,
            // @ts-ignore
            user_id: undefined
        }
    }
}
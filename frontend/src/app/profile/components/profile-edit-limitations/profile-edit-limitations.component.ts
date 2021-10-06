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
    limitations: UserLimitations = this.model ?? this.getEmptyLocation()

    onModelChange( $event: UserLimitations )
    {
        this.modelChange.emit( $event )
    }

    getEmptyLocation(): UserLimitations
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
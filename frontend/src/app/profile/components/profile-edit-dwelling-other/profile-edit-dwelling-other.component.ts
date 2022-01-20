import { Component, EventEmitter, Input, Output } from '@angular/core'


@Component( {
    selector: 'app-profile-edit-dwelling-other',
    templateUrl: './profile-edit-dwelling-other.component.html',
    styleUrls: [ './profile-edit-dwelling-other.component.scss' ]
} )
export class ProfileEditDwellingOtherComponent
{
    @Input() model!: any
    @Output() modelChange = new EventEmitter<any>()

    constructor()
    {
        this.model = this.model
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}

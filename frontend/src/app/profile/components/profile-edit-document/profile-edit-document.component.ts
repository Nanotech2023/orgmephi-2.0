import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Document, DocumentRF } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-document',
    templateUrl: './profile-edit-document.component.html',
    styleUrls: [ './profile-edit-document.component.scss' ]
} )
export class ProfileEditDocumentComponent
{
    @Input() model!: DocumentRF
    @Output() modelChange = new EventEmitter<Document>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}
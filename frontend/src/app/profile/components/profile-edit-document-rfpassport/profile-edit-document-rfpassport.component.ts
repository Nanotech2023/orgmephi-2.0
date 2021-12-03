import { Component, EventEmitter, Input, Output } from '@angular/core'
import { DocumentRF } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-document-rfpassport',
    templateUrl: './profile-edit-document-rfpassport.component.html',
    styleUrls: [ './profile-edit-document-rfpassport.component.scss' ]
} )
export class ProfileEditDocumentRfpassportComponent
{
    @Input() model!: DocumentRF
    @Output() modelChange = new EventEmitter<DocumentRF>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}

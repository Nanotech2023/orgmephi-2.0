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

    codePattern: string = "^[0-9]{3}-[0-9]{3}$"
    numberPattern: string = "^[0-9]{6}$"
    seriesPattern: string = "^[0-9]{4}$"

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}

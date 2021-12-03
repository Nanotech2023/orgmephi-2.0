import { Component, EventEmitter, Input, Output } from '@angular/core'
import { DocumentBirthCertificate } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-document-birthcertificate',
    templateUrl: './profile-edit-document-birthcertificate.component.html',
    styleUrls: [ './profile-edit-document-birthcertificate.component.scss' ]
} )
export class ProfileEditDocumentBirthcertificateComponent
{
    @Input() model!: DocumentBirthCertificate
    @Output() modelChange = new EventEmitter<DocumentBirthCertificate>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}

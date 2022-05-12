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

    numberPattern: string = "^[0-9]{6}$"
    seriesPattern: string = "^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})-[\u0410\-\u042F]{2}$"
    insurancePolicyPattern: string = "^[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}$"

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}

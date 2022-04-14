import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { DocumentRFInternational } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-document-rfinternationalpassport',
    templateUrl: './profile-edit-document-rfinternationalpassport.component.html',
    styleUrls: [ './profile-edit-document-rfinternationalpassport.component.scss' ]
} )
export class ProfileEditDocumentRfinternationalpassportComponent
{
    @Input() model!: DocumentRFInternational
    @Output() modelChange = new EventEmitter<DocumentRFInternational>()

    numberPattern: string = "^[0-9]{7}$"
    seriesPattern: string = "^[0-9]{2}$"

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}

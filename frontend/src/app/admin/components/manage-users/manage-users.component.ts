import { Component, ElementRef, OnInit, ViewChild } from '@angular/core'
import { ResponseUserAll } from '@/auth/api/models'
import { Observable } from 'rxjs'
import { fixedHeight } from '@/shared/consts'
import { AuthService } from '@/auth/api/auth.service'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )


export class ManageUsersComponent implements OnInit
{
    users$!: Observable<ResponseUserAll>
    minContainerHeight = fixedHeight
    @ViewChild( 'modal' ) modal!: ElementRef
    columnDefs = [
        { field: 'id', sortable: true, filter: true, headerName: 'ID' },
        { field: 'username', sortable: true, filter: true, headerName: 'Имя пользовтаеля' },
        { field: 'role', sortable: true, filter: true, headerName: 'Роль' },
        { field: 'type', sortable: true, filter: true, headerName: 'Тип регистрации' },
        { headerName: 'Действия' }
    ]
    modalVisible: boolean = false

    constructor( private service: AuthService ) { }

    ngOnInit(): void
    {
        this.users$ = this.service.userAllGet()
    }

    onClick( $event: any )
    {
        if ( $event.target == this.modal?.nativeElement )
            this.modalVisible = false
    }
}
